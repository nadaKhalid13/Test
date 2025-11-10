import random
matrix=['rock' , 'paper', 'scissors ']
print('welcome to the rock (@@@), paper(###), scissors ($$$) game:')
name= input('what is your name?')
a=input('press enter to continue or type (help) for rules help').lower()
if a =='help':
    print('           ##### Rules #####\n      1)you choose and computer choose')
    print('      2)Rock smashes scissors--> Rock win\n      3)scissors cut paper-->scissors win\n      4)paper cover rock-->paper win')
elif a == input():
   print('good, let continue') 
else :
    print(f'{a} invalid choose')
choiceguy =input('what you choose?').lower()
choicecomputer=random.choice(matrix)
if choiceguy == 'paper' and choicecomputer=='rock' or choiceguy == 'rock' and choicecomputer=='scissors' or choiceguy == 'scissors' and choicecomputer=='paper':
    print(f'your choice is-->{choiceguy}\ncomputer choice-->{choicecomputer}\n   you win, computer lose ')
elif choiceguy == 'paper' and choicecomputer=='scissors' or choiceguy == 'rock' and choicecomputer=='paper' or choiceguy == 'scissors' and choicecomputer=='rock':
    print(f'your choice is-->{choiceguy}\ncomputer choice-->{choicecomputer}\n   you lose, computer win ')
else :
    print(f'{choiceguy} {choicecomputer}, invalid choose') 