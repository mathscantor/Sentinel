import hashlib

'''
Obviously, you have come to try and get the answers from the answer engine. 
We have the md5 hash of this file to check for its integrity. 
Therefore, it is futile to replace the our hashes with your own hashes to score some ezpz points.
Good try :)
'''
class AnswerEngine:
    
    def __init__(self):
        self.answer_sha512_mapping = { 
            1: ["ca4ee0cc4c127a9d63ebad6dbabc39e373bf0ce9f24f5feb7d7d24dc823fec6a2f0d48fdecfdc5618e4e5af1685bbde23d41d60b5b1f4ff2b5f63989724d502c", False],
            2: ["69f1b22b6839edc3fc0cd1843d80876413d000f3715a59a03f646eddabdd796bcfb71e48d50426f850fb1bdcc9bd2c6b8ff100835d2377be3107a25646927835", False],
            3: ["3233dd6d542d248ff5c4a3588fdf8bf2febacb1daf26df6d0f04793835d74f1f8de05928c0770d1fe5e067aeb5de3919c42137a44cdc3d4294fe2dd1e353dad7", False],
            4: ["d0a748e8489374d8e7aa4a25e58b57d24ec556a5d56dea63ee6b9e3b0ae9740d9fe581d0838b921d1e2fe0c315d6a99167eab2e64192ad97d61cc2a9aa3febe7", False],
            5: ["04f77cf56adf6d3e83f0192339fad30f5fa1368b205754a300de2c6a7370b1e5f10e6b08a5d4426da30f0f9f8244d2635d61e251e11de6e86ef5a87f8a3ce6ae", False],
            6: ["ecdf7bba63c76ab882a843ea1827474982b0fc286762ac2f9e113b57c660367aeb218d4f469c72006d08e2948553db24975d443ecf31b5be3eb54fcc07379e75", False],
            7: ["98ac88f69470baadb795b464c7ea696e7052faaa7ec65c01416799d013cf8fcf0003adb1fbb8655d8319bf03e4a5811f6d256e31b7be426bad2c530317bff84b", False],
            8: ["c16db7f3a868a809c406eb622e0d5e8c2b170b0edb6cc56b712e6f8ab035465ca9450fbb2bab1c8664cdac671f08d62411a4e426b72eb2e484b46f9dd1f4d82f", False],
            9: ["0619a1114922cd0772d90987a41de63011ebfd979694a364c2044ed936fa2e4b5ffffcfb5b37d73c022778fa6a7f7f2573ffd009332309ca1156bea6785aedb3", False],
            10: ["a2a4af145419ee1f6439ea950ab0ac1116853198762f05a00304b374d2dc4875942f22c7a601a2b7b360c454d0549bb56f402a3a629c05dbf4a19af55da670db", False],
            11: ["7c2ade6096c8e638b3d01c427b459fbc57a5db238df6010cec6f238d3053ed09bdcaadf2c8ad985c899114f1e43c04dfd99b790c9f01a1714b10c30d3168a8b6", False],
            12: ["8335bfe4fc0b730cdd17ca41bdcd7382a1807bc29c456a3aa7353a3fc5af2817f95131573c69679c8932599ac6922ca6f9b247dc647e33bd52eb2e1115ae7881", False]
            
                                     }        
    def check_answer(self, question_no: int, answer: str):
        if hashlib.sha512(r"{}".format(answer).encode("utf-8") ).hexdigest() == self.answer_sha512_mapping[question_no][0]:
            print("Correct! Please proceed to the next question :)")
            self.answer_sha512_mapping[question_no][1] = True
        else:
            print("Wrong! Please try again :(")
            self.answer_sha512_mapping[question_no][1] = False
            
    def get_score(self) -> str:
        points = 0
        for question_no in self.answer_sha512_mapping:
            if self.answer_sha512_mapping[question_no][1]:
                points += 1
        
        return "Score: {} / {}".format(points, len(self.answer_sha512_mapping.keys()))