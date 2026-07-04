% order5v2_1902  eq1=23543 eq2=29439  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(X,f(X,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(Y,f(Z,f(W,Z)))),Y) )).
