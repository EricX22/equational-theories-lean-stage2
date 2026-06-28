% hard3_0298  eq1=2831 eq2=4385  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,Z)),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(X,X)) = f(f(Y,X),X) )).
