import random

def shutudai(a,QS):
    return QS[a]
def kaitou(ANS,ans):
    if ans in ANS:
        return "正解！！！"
    else:
        return "出直してこい"

if __name__ == "__main__":
    a = random.randint(0,2)
    QS = ["サザエの旦那の名前は？","カツオの妹の名前は？","タラオはカツオから見てどんな関係？"]
    ANS = {0:["マスオ","ますお"],1:["ワカメ","わかめ"],2:["甥","おい","甥っ子","おいっこ"]}

    print(f"問題：\n{shutudai(a,QS)}")
    ans = input("答えるんだ：")
    print(kaitou(ANS[a],ans))