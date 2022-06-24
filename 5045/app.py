from flask import Flask

app = Flask(__name__)

class GlobalTest():
    __count = 1

    @classmethod
    def main(self):
        self.__count += 1
        return self.__count

@app.route("/")
def hello_world():

    return f"{GlobalTest.main()}"

app.run('0.0.0.0', 8000)