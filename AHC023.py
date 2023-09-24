from enum import Enum
from typing import List
import io
import sys
import glob
from collections import deque
from heapq import heappop, heappush
from random import shuffle, randint

prob=[0.00753, 0.03362, 0.08225, 0.14909, 0.22675, 0.30829, 0.38856, 0.46425, 0.53356, 0.59574, 0.65071, 0.69881, 0.74058, 0.77668, 0.80776, 0.83446, 0.85735, 0.87697, 0.89378, 0.90818, 0.92053, 0.93113, 0.94022, 0.94805, 0.95478, 0.96058, 0.96559, 0.96991, 0.97366, 0.97690, 0.97972, 0.98216, 0.98430, 0.98615, 0.98777, 0.98919, 0.99043, 0.99152, 0.99247, 0.99331, 0.99405, 0.99470, 0.99528, 0.99578, 0.99623, 0.99663, 0.99698, 0.99730, 0.99758, 0.99782, 0.99805, 0.99824, 0.99842, 0.99858, 0.99872, 0.99884, 0.99895, 0.99906, 0.99915, 0.99923, 0.99930, 0.99937, 0.99943, 0.99948, 0.99953, 0.99958, 0.99962, 0.99965, 0.99968, 0.99971, 0.99974, 0.99977, 0.99979, 0.99981, 0.99983, 0.99984, 0.99986, 0.99987, 0.99988, 0.99990, 0.99991, 0.99992, 0.99993, 0.99993, 0.99994, 0.99995, 0.99995, 0.99996, 0.99997, 0.99997, 0.99997, 0.99998, 0.99998, 0.99999, 0.99999, 0.99999, 1.00000, 1.00000, 1.00000]

#同じフォルダにtest_caseという名称でテストケースを置けば、test関数等が動く
path='C:/Users/katonyonko/OneDrive/デスクトップ/AHC023'
files = sorted(glob.glob(path+"/test_case/*"))

class Ahc023:
  eval=0
  def __init__(self,T,H,W,i0,h,v,K,SD):
    #入力
    self.T=T
    self.H=H
    self.W=W
    self.i0=i0
    self.h=h
    self.v=v
    self.K=K
    self.SD=SD

    #盤面のどこにいつ出ていく作物が置いてあるか
    self.field = [0]*self.H*self.W

    #答え
    self.ans=[]
    self.tmp_ans=[]
    self.cur_score=0
  
  def idx(self,i,j):
    return i*self.W+j

  def bfs(self):
    dist = [200]*self.H*self.W
    dist[self.idx(self.i0,0)]=0
    dq=deque([self.idx(self.i0,0)])
    while dq:
      x=dq.popleft()
      for y in self.G[x]:
        if self.field[y]>0: continue
        if dist[y]>dist[x]+1:
          dist[y]=dist[x]+1
          dq.append(y)
    return dist

  def keep_connect(self,i,j):
    if self.field[self.idx(i,j)]>0:
      return 0
    else:
      #vの中に一個でもダメなものがあったら0
      for v in self.G[self.idx(i,j)]:
        if self.dist[v]<self.dist[self.idx(i,j)] or self.field[v]>0: continue
        tmp=0
        #wの中に一個でもOKなものがあったらこのvはOK
        for w in self.G[v]:
          if self.field[w]==0 and w!=self.idx(i,j) and self.dist[w]==self.dist[self.idx(i,j)]:
            tmp=1
        if tmp==0:
          return 0
      if len([1 for v in self.G[self.idx(i,j)] if self.field[v]==0])==4: return 0
      return 1
    
  def put_crops(self,i,j,d):
    #1つでもダメなものがあったら0
    for v in self.G[self.idx(i,j)]:
      if self.field[v]==0 or self.field[v]>d: continue
      tmp=0
      #wのどれかに抜けられたらOK
      for w in self.G[v]:
        if w!=self.idx(i,j) and self.field[w]<self.field[v]:
          tmp=1
      if tmp==0:
        return 0
    return 1
  
  def sort_crops(self):
    return sorted([(self.SD[i][0],self.SD[i][1],i) for i in range(self.K)],key=lambda x:(x[0],-x[1]))

  def prepare(self):
    self.G=[set() for _ in range(self.H*self.W)]
    for i in range(self.H-1):
      for j in range(self.W):
        if self.h[i][j]=="0":
          self.G[self.idx(i,j)].add(self.idx(i+1,j))
          self.G[self.idx(i+1,j)].add(self.idx(i,j))
    for i in range(self.H):
      for j in range(self.W-1):
        if self.v[i][j]=="0":
          self.G[self.idx(i,j)].add(self.idx(i,j+1))
          self.G[self.idx(i,j+1)].add(self.idx(i,j))
    self.dist = self.bfs()
    self.order=sorted(self.dist)
    self.max_dist=max(self.dist)
    self.dist_idx=[[] for _ in range(self.max_dist+1)]
    tmp=list(range(self.H*self.W))
    shuffle(tmp)
    for i in tmp:
      self.dist_idx[self.dist[i]].append(i)
    # self.dist_idxは後で外重視に並べ替えたい
    self.use_crops=self.sort_crops()

  def find(self,p):
    return self.order[max(0,min(int(self.H*self.W*p)+randint(-2,2)-1,self.H*self.W-1))]
  
  def put(self,t,i):
    d=self.SD[i][1]
    p=prob[d-t-1]/prob[self.T-t-1]
    shd=self.find(p)
    for v in self.dist_idx[shd]:
      if self.keep_connect(v//self.W,v%self.W)==1 and self.put_crops(v//self.W,v%self.W,d)==1:
        self.field[v]=d
        self.tmp_ans.append(' '.join(map(str,[i+1,v//self.W,v%self.W,t])))
        return 1
    for j in range(1,self.max_dist+1):
      if shd-j<0 and shd+j>self.max_dist: break
      for k in [-j,j]:
        if shd+k<0 or shd+k>self.max_dist: continue
        for v in self.dist_idx[shd+k]:
          if self.keep_connect(v//self.W,v%self.W)==1 and self.put_crops(v//self.W,v%self.W,d)==1:
            self.field[v]=d
            self.tmp_ans.append(' '.join(map(str,[i+1,v//self.W,v%self.W,t])))
            return 1
    return 0
  
  def solve(self):
    for _ in range(3):
      self.prepare()
      kouho=[]
      for t in range(1,self.T+1):
        while len(self.use_crops)>0 and self.use_crops[0][0]<=t:
          s,d,i=self.use_crops.pop(0)
          heappush(kouho,(-d,i))
        nxt=[]
        while kouho:
          d,i=heappop(kouho)
          available=self.put(t,i)
          if available==0 and s<t: heappush(nxt,(-d,i))
        for k in range(self.H*self.W):
          if self.field[k]==t:
            self.field[k]=0
        self.dist = self.bfs()
        kouho=nxt
      tmp_score=self.score(self.tmp_ans)
      if tmp_score>self.cur_score:
        self.ans=self.tmp_ans
        self.cur_score=tmp_score
      self.tmp_ans=[]

  def score(self,ans):
    res=0
    for x in ans:
      k,i,j,s=map(int,x.split(" "))
      res+=self.SD[int(k)-1][1]-self.SD[int(k)-1][0]+1
    return res

  def write(self,i):
    self.writefile = open(path+'/output/'+str(i).zfill(4)+'output.txt', 'w')
    self.writefile.write(str(len(self.ans))+"\n")
    self.writefile.write("\n".join(self.ans))

def main(i):
  if i>=0:
    with open(files[i]) as f:
      lines = f.read()
      sys.stdin = io.StringIO(lines)
  T,H,W,i0 = [int(v) for v in input().split(" ")]
  h=[input() for _ in range(H-1)]
  v=[input() for _ in range(H)]
  K=int(input())
  SD=[list(map(int,input().split())) for _ in range(K)]
  solver = Ahc023(T,H,W,i0,h,v,K,SD)
  solver.solve()
  if i>=0: solver.write(i)
  else: print("\n".join([str(len(solver.ans))]+solver.ans))

def test(s,g):
  for i in range(s,g):
    main(i)
  print(Ahc023.eval/(g-s)*50)

if __name__ == "__main__":
  flg=0
  if flg==0: main(-1)
  elif flg==1: test(0,1)