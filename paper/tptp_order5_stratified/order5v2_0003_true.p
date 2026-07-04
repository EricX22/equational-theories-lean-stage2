% order5v2_0003  eq1=8131 eq2=6340  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,f(Z,W)),Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(f(Y,Y),Y)))) )).
