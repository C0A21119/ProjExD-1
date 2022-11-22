if __name__ == "__main__":
    import random

    def shutudai(a):
        QS = ["サザエの旦那の名前は？","カツオの妹の名前は？","タラオはカツオから見てどんな関係？"]
        return QS[a]
    def kaitou(a,ans):
        ANS = [["マスオ","ますお"],["ワカメ","わかめ"],["甥","おい","甥っ子","おいっこ"]]
        if ans in ANS[a]:
            return "正解！！！"
        else:
            return "出直してこい"

    a = random.randint(0,2)
    print(f"問題：\n{shutudai(a)}")
    ans = input("答えるんだ：")
    print(kaitou(a,ans))