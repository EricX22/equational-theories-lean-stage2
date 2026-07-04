% order5_0220  eq1=27119 eq2=31320  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,W)),f(U,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(f(X,Z),f(Z,Y))),X) )).
