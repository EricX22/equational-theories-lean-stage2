% order5_0110  eq1=39516 eq2=30850  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(Y,Z),f(Y,Z)),X),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(f(Z,W),Z))),Z) )).
