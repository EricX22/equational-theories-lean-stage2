% order5v2_1312  eq1=23741 eq2=13173  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),Y),f(Z,f(W,Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(Y,f(X,X))),W)) )).
