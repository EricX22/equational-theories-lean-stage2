% order5v2_0868  eq1=30020 eq2=20027  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,f(Y,Y)))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(Y,f(Z,W)),X)) )).
