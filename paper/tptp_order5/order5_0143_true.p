% order5_0143  eq1=57530 eq2=831  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,f(Y,X)) = f(f(f(X,Y),X),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(f(X,Y),f(Z,W))) )).
