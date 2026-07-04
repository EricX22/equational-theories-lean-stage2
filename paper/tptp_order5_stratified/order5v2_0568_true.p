% order5v2_0568  eq1=18423 eq2=18426  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(X,f(f(W,W),Z))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(X,f(f(W,U),X))) )).
