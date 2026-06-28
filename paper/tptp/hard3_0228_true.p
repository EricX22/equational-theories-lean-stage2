% hard3_0228  eq1=2086 eq2=56  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(X,Y),Z),f(W,U)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(Y,f(Y,Y))) )).
