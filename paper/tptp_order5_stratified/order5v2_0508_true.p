% order5v2_0508  eq1=31337 eq2=16463  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(X,Z),f(W,X))),U) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(f(f(f(Y,X),Y),Y),X)) )).
