import llama_cpp
import sys
import re
import signal
import imp
from alive_progress import alive_bar
import socket
import threading
import time

HEADER = 2000000000
PORT = 5050
SERVER = "192.168.0.104"  # socket.gethostbyaddr("13.41.72.251")[0]
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

try:
    imp.find_module("config")
    from config import *
except ImportError:
    print("Cannot find config.py")
    print('Make sure that you copy "config.example.py" to "config.py"')
    exit(1)

model = llama_cpp.Llama(
    model_path=MODEL_PATH,
    seed=SEED,
    n_threads=N_THREADS,
    last_n_tokens_size=N_LAST_TOKENS,
    n_ctx=N_CTX,
)

TOKEN_BOS = model.token_bos()
TOKEN_EOS = model.token_eos()

PROMPT_INIT = f""" {PERSONA_DESC}

Pretend that you are {PERSONA_NAME}. Below is an instruction that describes a task. Write a response that appropriately completes the request.""".encode()

is_received_stop_signal = False  # TODO: catching SIGINT signal


def init():
    global state_after_init_prompt
    print("")
    m_eval(model, m_tokenize(model, PROMPT_INIT, True), False, "Starting up...")
    print("[SERVER STARTED]")
    server.listen()
    print(f"[LISTENING] {SERVER}")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
            print("\n> ", end="", flush=True)

    except KeyboardInterrupt:
        pass


###########################################


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] from {addr}")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            input_txt = msg
            process_user_input(input_txt, conn, addr)
            # print(response_added_bytes.decode(errors="ignore"), end="", flush=True)

    conn.close()


###########################################


def process_user_input(text, conn, addr):
    global state_after_init_prompt, is_received_stop_signal
    is_received_stop_signal = False

    # generate response
    response_bytes = b""
    response_txt = ""
    input_tokens = m_tokenize(
        model, (f"\n\n### Instruction:\n\n{text}\n\n### Response:\n\n").encode()
    )
    for token in m_generate(
        model,
        input_tokens,
        top_k=TOP_K,
        top_p=TOP_P,
        temp=TEMP,
        repeat_penalty=REPEAT_PENALTY,
    ):
        if token == TOKEN_EOS:
            break
        should_stop = False
        response_added_bytes = model.detokenize([token])
        response_bytes += response_added_bytes
        response_txt = response_bytes.decode(errors="ignore")
        if "###" in response_txt:
            response_txt = re.sub(r"\s+###", "", response_txt)
            sys.stdout.write("\033[K")  # Clear to the end of line
            print(response_txt.split("\n")[-1], end="", flush=True)
            should_stop = True

        response = response_added_bytes.decode(errors="ignore")
        print(response, end="", flush=True)
        if should_stop:
            break
        conn.send(response.encode(FORMAT))

    # build context for next message
    end = "-"
    input_ins_truncated = " ".join(text.split(" ")[:N_TOKENS_KEEP_INS])
    input_res_truncated = " ".join(response_txt.split(" ")[:N_TOKENS_KEEP_RES])
    input_history = f"\n\n### Instruction:\n\n{input_ins_truncated}\n\n### Response:\n\n{input_res_truncated}"

    history_tokens = m_tokenize(model, input_history.encode())
    print("\n\n", end="", flush=True)
    m_eval(model, history_tokens, False, "Build context...")
    conn.send(end.encode(FORMAT))


def m_generate(model: llama_cpp.Llama, tokens, top_k, top_p, temp, repeat_penalty):
    """Generate without self.reset()"""
    global is_received_stop_signal
    is_received_stop_signal = False
    try:
        while True:
            if is_received_stop_signal:
                yield TOKEN_EOS
            m_eval(model, tokens, True)
            token = model.sample(
                top_k=top_k,
                top_p=top_p,
                temp=temp,
                repeat_penalty=repeat_penalty,
            )
            tokens_or_none = yield token
            tokens = [token]
            if tokens_or_none is not None:
                tokens.extend(tokens_or_none)

    except KeyboardInterrupt:
        pass


def m_tokenize(model: llama_cpp.Llama, text: bytes, add_bos=False):
    assert model.ctx is not None
    n_ctx = llama_cpp.llama_n_ctx(model.ctx)
    tokens = (llama_cpp.llama_token * int(n_ctx))()
    n_tokens = llama_cpp.llama_tokenize(
        model.ctx,
        text,
        tokens,
        n_ctx,
        llama_cpp.c_bool(add_bos),
    )
    if int(n_tokens) < 0:
        raise RuntimeError(f'Failed to tokenize: text="{text}" n_tokens={n_tokens}')
    return list(tokens[:n_tokens])


def m_eval(model: llama_cpp.Llama, tokens, stop_on_signal=False, show_progress=False):
    global is_received_stop_signal

    def chunks(lst, n):
        return [lst[i : i + n] for i in range(0, len(lst), n)]

    batches = chunks(tokens, N_BATCH)

    def __eval(bar=None):
        global is_received_stop_signal
        for i, batch in enumerate(batches):
            if stop_on_signal and is_received_stop_signal:
                is_received_stop_signal = False
                return
            else:
                model.eval(batch)
                bar(len(batch)) if bar is not None else None

    if show_progress:
        with alive_bar(len(tokens), theme="classic", title=show_progress) as bar:
            __eval(bar)
    else:
        __eval()


init()
