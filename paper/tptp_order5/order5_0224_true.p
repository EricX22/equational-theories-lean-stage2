% order5_0224  eq1=23182 eq2=61799  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,Y),X),f(Y,f(Z,Z))) )).
fof(goal, conjecture, ! [X,Y] : ( f(f(X,X),Y) = f(f(f(Y,Y),X),X) )).
