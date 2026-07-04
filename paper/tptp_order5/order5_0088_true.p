% order5_0088  eq1=36918 eq2=9885  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),f(W,W)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(Z,f(W,Z)))) )).
