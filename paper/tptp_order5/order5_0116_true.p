% order5_0116  eq1=6517 eq2=58564  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(Y,f(f(X,Y),f(Z,X)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,Y),Y) = f(X,f(Y,f(Z,Z))) )).
