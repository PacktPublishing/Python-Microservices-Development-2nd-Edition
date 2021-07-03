import jwt


def create_token(alg="HS256", secret="secret", data=None):
    return jwt.encode(data, secret, algorithm=alg)


def read_token(token, secret="secret", algs=["HS256"]):
    return jwt.decode(token, secret, algorithms=algs)


token = create_token(data={"some": "data", "inthe": "token"})

print(token)
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoiZGF0YSIsImludGhlIjoidG9rZW4ifQ.vMHiSS_vk-Z3gMMxcM22Ssjk3vW3aSmJXQ8YCSCwFu4
print(read_token(token))
