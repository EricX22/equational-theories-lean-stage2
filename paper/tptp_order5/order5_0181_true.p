% order5_0181  eq1=42106 eq2=172  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(X,f(W,f(U,Y)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,X),f(Z,X)) )).
