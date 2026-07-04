% order5_0050  eq1=13873 eq2=2630  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(f(Y,Y),Z)),Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,W),Z)),Z) )).
