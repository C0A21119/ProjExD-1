import random
import datetime

def code(n):
    subject_list = []
    for i in range(n):
        subject_list += [chr(random.randint(65,90))]
    print("対象文字：")
    print(" ".join(subject_list))
    return subject_list
def ans(n,subject_list):
    ans_list = []
    for i in range(n):
        ans_list += [subject_list.pop()]
        random.shuffle(subject_list)
    print("欠損文字:")
    print(" ".join(ans_list))
    print("表示文字:")
    print(" ".join(subject_list))
    return ans_list

def much(ans_list):
    i = 1
    tf = True
    if len(ans_list) == int(input("欠損文字はいくつあるでしょうか？")):
        print("正解です。それでは、具体的に欠損文字を1つずつ入力してください")
        while tf:
            ans = input(f"{i}つ目の文字を入力してください")
            if ans in ans_list:
                ans_list.remove(ans)
                i+=1
                if not ans_list:
                    print("全問正解おめでとう")
                    tf = False
                    return tf
            else:
                print("不正解です。またチャレンジしてください")
                return tf
    else:
        print("不正解です。またチャレンジしてください")
        return tf

if __name__ == "__main__":
    f = True
    i = 1
    num = 3
    st = datetime.datetime.now()
    poit = random.randint(3,10)
    tagt = random.randint(1,4)
    while f:
        print(f"{i}回目")
        tagt_list = code(poit)
        ans_list = ans(tagt,tagt_list)
        f = much(ans_list)
        i += 1
        if num == i:
            break
    ed = datetime.datetime.now()
    print(f"{i}回目、time:{(ed-st)}  成功です")