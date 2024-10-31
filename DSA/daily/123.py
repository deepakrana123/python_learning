class Solution:
    def solve(self,i,j,index,word,board):
        dirs=[[-1, 0],[1, 0],[0, -1], [0, 1]]
        if index==len(word):
            return True
        if i<0 or i>=len(board) or j<0 or j>=len(board[0]) or board[i][j]=='$':
            return False 
        if board[i][j]!=word[index]:
            return False
        temp=board[i][j]
        board[i][j]='$'
        for d in dirs:
            x,y=d[0],d[1]
            if self.solve(i+x,j+y,index+1,word,board):
                return True
        board[i][j]=temp
        return False
    def exist(self, board: List[List[str]], word: str) -> bool:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j]==word[0] and self.solve(i,j,0,word,board):
                    return True
        return False
        