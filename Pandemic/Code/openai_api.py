import openai
import os
from dotenv import load_dotenv
import tkinter as tk
# Variables and initiators


class OPENAI_API():

  def __init__(self):
    load_dotenv()
    self.start_sequence = "\nAI:"
    self.restart_sequence = "\nHuman: "
    openai.api_key = os.getenv('OPENAI_API_KEY')
    self.session_prompt = "The following is a deep conversation with an AI that is helpful, creative, very clever, and very friendly."
    self.chat_log = None
    self.question = None

    #Tkinter
    self.root = tk.Tk()
    self.root.geometry("500x500")

    #Variables
    self.q = tk.StringVar()
    self.entry = tk.Entry(self.root, textvariable=self.q, width=65, relief = tk.GROOVE)

    self.a = tk.StringVar()
    self.a.set('IA:')
    self.label = tk.Label(self.root, textvariable=self.a,  font=(None, '14'),justify=tk.LEFT)

    self.entry.place(x=50, y=50)
    self.label.place(x=20, y=80)

    send_button = tk.Button(text='Send', relief = tk.GROOVE,command= lambda : self.get_entry_value_for_question(), height = 1, width = 10)
    send_button.place(x=400, y=450)

    self.root.mainloop()
  
  def ask(self):

      if self.chat_log is None:
        self.chat_log = self.session_prompt
      prompt_text = f'{self.chat_log}{self.restart_sequence}: {self.question}{self.start_sequence}:'

      response = openai.Completion.create(
          model="text-davinci-002",
          prompt=prompt_text,
          temperature=0.9,
          max_tokens=150,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0.6,
          stop=[" Human:", " AI:"]
          )
      
      story = response['choices'][0]['text']
      return str(story)

  def append_interaction_to_chat_log(self, answer):
      return f'{self.chat_log}{self.restart_sequence} {self.question}{self.start_sequence}{answer}'

  def talk(self):
    answer = self.ask()
    answer = self.process_txt(answer)
    self.a.set(f'IA: {answer}')
    self.chat_log = self.append_interaction_to_chat_log(answer)

  def process_txt(self, answer):
    
    new_ans = ''''''
    for line in answer.split('.'):
        new_ans = new_ans+f'\n {line}.'
    return new_ans
      
  def get_entry_value_for_question(self):
    if self.q.get():
      self.question = self.q.get()
      self.q.set('')
      self.talk()
    

if __name__ == '__main__':
  
  while True:
    api = OPENAI_API()
    

