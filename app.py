import redis
from flask import Flask
from rq import Queue
from rq.job import Job
from flask import request

conn = redis.from_url("redis://@localhost:6379/0")
q = Queue(connection=conn)

app = Flask(__name__)


def transfer_request_to_bank_b(account_id, transfer_amount):
    print(f"Sending request to Bank B")
    return True

@app.route("/", methods=['POST'])
def post_transaction():
    request_data = request.json()
    account_id = request_data["account_id"]
    transfer_amount = request_data["amount"]
    job = q.enqueue_call(
        func=transfer_request_to_bank_b, args=(account_id,transfer_amount,), result_ttl=5000
    )
    return job.get_id()


@app.route("/result/", methods=['GET'])
def get_result(job_id):
    job = Job.fetch(job_id, connection=conn)
    if job.is_finished:
        return "Transfer Complete"
    return "Transfer Pending"


if __name__ == "__main__":
    app.run()
