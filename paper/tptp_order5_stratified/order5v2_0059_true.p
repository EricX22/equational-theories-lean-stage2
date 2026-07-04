% order5v2_0059  eq1=23839 eq2=8010  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),Z),f(W,f(W,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(Z,f(f(Z,f(Y,Z)),X))) )).
