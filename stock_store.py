import sys
import math
import tkinter.messagebox as msbox
import time
import tkinter.ttk as ttk
from tkinter import *
from random import *
import threading
import json
from typing import List

root = Tk()
root.title('재고_관리')
root.geometry('640x480+800+100') # 가로 * 세로 + x좌표 + y좌표

search_frame = Frame(root)
search_frame.grid(row=0,column=0)
output_frame = Frame(root)
output_frame.grid(row=1,column=0)
input_frame = Frame(root)
input_frame.grid(row=2,column=0)
delete_frame = Frame(root)
delete_frame.grid(row=3,column=0)

###################출력_프레임###############################

#jsonfile write
def python_json():
    global store_dic_board
    try:
        with open('stock_store.json', 'w', encoding= 'utf-8') as json_write :
            json.dump(store_dic_board, json_write, indent=5, ensure_ascii=False)
#        print('store_dic_board_input_j',store_dic_board)
    except:
        print('input_error')
#    store_dic_board = json.dumps(json_write, indent=5, sort_keys=True)

#jsonfile read
def json_python():
    global store_dic_board, store_board # 1. back, 2. front
    try:
        with open('stock_store.json', 'r', encoding='utf-8') as json_read :
            store_dic_board = json.load(json_read)
#        print('store_dic_board_outcome_j',store_dic_board)  
    except:
        store_dic_board = {"list" : [{"type" : "제품명", "manufactor" : "제조사", "count" : "숫자"}]}
#    store_board = store_dic_board

#제이슨에서 파이썬으로 가져오기
json_python()
#파이썬에서 제이슨으로 집어넣기
python_json()


#화면에 띄울 함수 선언
def make_list():
    global sort_dic, store_board, store_dic_board
    ##store_dic_board 정렬
    sort_dic = store_dic_board["list"]
    #value값만 가져오기
    store_board = sort_dic.copy()
def make_json():
    global sort_dic, store_board, store_dic_board
    ##store_dic_board 정렬
    sort_dic = store_board
    #value값만 가져오기
    store_dic_board["list"] = sort_dic.copy()

#리스트 만들기
make_list()
# for i in store_dic_board.values:
#     store_board.append(i)


#print(store_board)

#화면에 띄우기
def board_print():
    txt.configure(state='normal')
    txt.delete("1.0","end")
    for stock in store_board:
        txt.insert(END, stock['type'] + '-' + stock['manufactor'] + '-' + str(stock['count']) + '\n')
    txt.configure(state='disabled')


#스크롤바 생성
scrollbar = Scrollbar(output_frame)
scrollbar.pack(side='right', fill='y')
#txt 생성, 스크롤바에 연동
txt=Text(output_frame, yscrollcommand=scrollbar.set)
#화면에 자료 출력
board_print()
##마우스 우클릭 하면 수정_삭제 팝업 띄우도록 설정
#txt.bind('<Button-3>', revision_delete) #폐기
txt.pack(side='left',fill='both', expand=True)
#스크롤바를 txt에 연동
scrollbar.config(command=txt.yview)

#####################출력프레임#################################################







#########################검색프레임#############################################

#검색하고 결과를 화면에 띄우기
def search_result_show():
    global store_board, sort_dic, search_text
    store_board.clear()
    for um in sort_dic:
        if um['type'] == search_text or um['manufactor'] == search_text or um['count'] == search_text :
            store_board.append({"type" : um['type'], "manufactor" : um['manufactor'], "count" : um['count']})
    if not store_board:
        msbox.showerror('에러', '검색 결과가 없습니다.')
        return
    board_print()

#화면 초기화하기
def reset_board():
    global store_board, sort_dic
    store_board.clear()
    json_python()
    make_list()
    board_print()

#검색결과 받아오기
def get_search_input(event=None):
    global search_text, search_entry, search_result_show
    search_text = str(search_entry.get())
    search_entry.delete(0, 'end')
#    print(search_text)
    search_result_show()

#검색입력창 생성
#search_input = StringVar(root, value='')
search_entry = Entry(search_frame)
search_entry.grid(row=0, column = 0, sticky=N+E+W+S)
search_entry.bind('<Return>', get_search_input)

#검색버튼 생성
search_button = Button(search_frame, text='검색', width=5, height=2, command = lambda : get_search_input())
search_button.grid(row=0, column= 1, sticky=N+E+W+S)

#화면 초기화버튼 생성
reset_button = Button(search_frame, text='초기화', width=5, height=2, command = lambda : reset_board())
reset_button.grid(row=0, column= 2, sticky=N+E+W+S)


###################검색프레임#################################################




####################입력프레임################################################

#재고 추가 업데이트
def add_board():
    global store_dic_board, store_board, txt
    store_board.append({"type" : f"{type_text}", "manufactor": f"{manufactor_text}", "count": count_text})
#    print('보드에 추가', store_board)
    # txt.configure(state='normal')
    # txt.insert(END, f"\n {type_text}-{manufactor_text}-{count_text}")
    # txt.configure(state='disabled')
    make_json()
    python_json()
    json_python()
    board_print()



#커서가 입력창에 들어갔을때 반응 - 안을 공백으로 만든다
def button_click(event):
    if type_entry.get() == '제품':
        type_entry.delete(0, 'end')
    if manufactor_entry.get() == '제조사':
        manufactor_entry.delete(0, 'end')
    if count_entry.get() == '개수':
        count_entry.delete(0, 'end')
#커서가 입력창에서 빠져나갔을때 반응 - 내부가 비어있다면 원래대로 되돌린다. 입력커서도 함께 제거한다.
def button_out(event):
    if type_entry.get() == '':
        type_entry.insert(0, '제품')
        root.focus()
    if manufactor_entry.get() == '':
        manufactor_entry.insert(0, '제조사')
        root.focus()
    if count_entry.get() == '':
        count_entry.insert(0, '개수')
        root.focus()

#재고추가 버튼 눌렀을때 반응
def get_input():
    global type_text, manufactor_text, count_text, type_entry, manufactor_entry, count_entry, go_json
    #입력창 내부가 비어있으면 알림창 띄우기
    if type_entry.get() == '':
        msbox.showerror('에러','제품 입력을 확인해주세요.')        
        return
    if manufactor_entry.get() == '':
        msbox.showerror('에러','제조사 입력을 확인해주세요.')
        return
    if count_entry.get() == '':
        msbox.showerror('에러','개수 입력을 확인해주세요.')
        return
    #개수입력창에 소수점 입력될 기미가 있으면 알림창 띄우기
    if '.' in count_entry.get():
#        print(type(count_entry.get()))
        msbox.showerror('에러','정확한 숫자로 입력해주세요.')
        return
    #개수입력창에 문자가 입력되면 알림창 띄우기
    try:
        if type(int(count_entry.get())) != int:
        #    print(type(count_entry.get()), type(int(count_entry.get())), type(count_entry))
            msbox.showerror('에러','숫자로 입력해주세요.')
            return
    except:
        msbox.showerror('에러','숫자로 입력해주세요.')
        return
    #입력이 전부 돼있다면 json으로 집어넣을 dic생성
    type_text = str(type_entry.get())
    manufactor_text = str(manufactor_entry.get())
    count_text = str(count_entry.get())
    if type_text == '제품' or manufactor_text == '제조사' or count_text == '개수':
        msbox.showerror('에러', '입력창을 클릭해 주세요.')
        return
    type_entry.delete(0, 'end')
    manufactor_entry.delete(0, 'end')
    count_entry.delete(0, 'end')
    #확인
#    print('입력했을때', store_dic_board)
    add_board()

#제품엔트리박스 생성
type_entry = Entry(input_frame)
type_entry.grid(row=0, column=0, sticky=N+E+W+S)
type_entry.insert(0, '제품')
#외부요인에 반응
type_entry.bind('<Enter>', button_click)
type_entry.bind('<Leave>', button_out)
manufactor_entry = Entry(input_frame)
manufactor_entry.grid(row=0, column=1, sticky=N+E+W+S)
manufactor_entry.insert(0, '제조사')
manufactor_entry.bind('<Enter>', button_click)
manufactor_entry.bind('<Leave>', button_out)
count_entry = Entry(input_frame)
count_entry.grid(row=0, column=2, sticky=N+E+W+S)
count_entry.insert(0, '개수')
count_entry.bind('<Enter>', button_click)
count_entry.bind('<Leave>', button_out)

#재고입력버튼 생성
input_button = Button(input_frame, text='재고\n추가', width=5, height=2, command = lambda : get_input())
input_button.grid(row = 0, column = 3 , sticky=N+E+W+S)
###############입력프레임#####################################################


###############삭제프레임######################################################

#커서가 입력창에 들어갔을때 반응 - 안을 공백으로 만든다
def button_click_de(event):
    if type_entry_de.get() == '제품':
        type_entry_de.delete(0, 'end')
    if manufactor_entry_de.get() == '제조사':
        manufactor_entry_de.delete(0, 'end')
    if count_entry_de.get() == '개수':
        count_entry_de.delete(0, 'end')
#커서가 입력창에서 빠져나갔을때 반응 - 내부가 비어있다면 원래대로 되돌린다. 입력커서도 함께 제거한다.
def button_out_de(event):
    if type_entry_de.get() == '':
        type_entry_de.insert(0, '제품')
        root.focus()
    if manufactor_entry_de.get() == '':
        manufactor_entry_de.insert(0, '제조사')
        root.focus()
    if count_entry_de.get() == '':
        count_entry_de.insert(0, '개수')
        root.focus()

#재고추가 버튼 눌렀을때 반응
def get_delete():
    global type_text_de, manufactor_text_de, count_text_de, type_entry_de, manufactor_entry_de, count_entry_de, go_json, store_board, sort_dic, txt, store_dic_board
    #입력창 내부가 비어있으면 알림창 띄우기
    if type_entry_de.get() == '':
        msbox.showerror('에러','제품 입력을 확인해주세요.')        
        return
    if manufactor_entry_de.get() == '':
        msbox.showerror('에러','제조사 입력을 확인해주세요.')
        return
    if count_entry_de.get() == '':
        msbox.showerror('에러','개수 입력을 확인해주세요.')
        return
    #개수입력창에 소수점 입력될 기미가 있으면 알림창 띄우기
    if '.' in count_entry_de.get():
#        print(type(count_entry_de.get()))
        msbox.showerror('에러','정확한 숫자로 입력해주세요.')
        return
    #개수입력창에 문자가 입력되면 알림창 띄우기
    try:
        if type(int(count_entry_de.get())) != int:
#            print(type(count_entry_de.get()), type(int(count_entry_de.get())), type(count_entry_de))
            msbox.showerror('에러','숫자로 입력해주세요.')
            return
    except:
        msbox.showerror('에러','숫자로 입력해주세요.')
        return
    type_text_de = str(type_entry_de.get())
    manufactor_text_de = str(manufactor_entry_de.get())
    count_text_de = str(count_entry_de.get())
    if type_text_de == '제품' or manufactor_text_de == '제조사' or count_text_de == '개수':
        msbox.showerror('에러', '입력창을 클릭해 주세요.')
        return
    type_entry_de.delete(0, 'end')
    manufactor_entry_de.delete(0, 'end')
    count_entry_de.delete(0, 'end')
    
    #삭제할 데이터 검색
    store_board.clear()
    for jun in sort_dic:
        if str(jun['type']) == type_text_de and str(jun['manufactor']) == manufactor_text_de and str(jun['count']) == count_text_de:
            print('t'*30, jun['type'], type_text_de, 'm'*30, jun['manufactor'], manufactor_text_de, 'c'*30, jun['count'], count_text_de)
        else :
            store_board.append({"type" : jun['type'], "manufactor" : jun['manufactor'], "count" : jun['count']})
    make_json()
    python_json()
    json_python()
    make_list()
    board_print()

#제품엔트리박스 생성
type_entry_de = Entry(delete_frame)
type_entry_de.grid(row=0, column=0, sticky=N+E+W+S)
type_entry_de.insert(0, '제품')
#외부요인에 반응
type_entry_de.bind('<Enter>', button_click_de)
type_entry_de.bind('<Leave>', button_out_de)
manufactor_entry_de = Entry(delete_frame)
manufactor_entry_de.grid(row=0, column=1, sticky=N+E+W+S)
manufactor_entry_de.insert(0, '제조사')
manufactor_entry_de.bind('<Enter>', button_click_de)
manufactor_entry_de.bind('<Leave>', button_out_de)
count_entry_de = Entry(delete_frame)
count_entry_de.grid(row=0, column=2, sticky=N+E+W+S)
count_entry_de.insert(0, '개수')
count_entry_de.bind('<Enter>', button_click_de)
count_entry_de.bind('<Leave>', button_out_de)

#재고입력버튼 생성
input_button = Button(delete_frame, text='삭제', width=5, height=2, command = lambda : get_delete())
input_button.grid(row = 0, column = 3 , sticky=N+E+W+S)

###############삭제프레임######################################################



root.mainloop()