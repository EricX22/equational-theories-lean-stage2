% order5v2_1875  eq1=5399 eq2=49739  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Z,f(Z,f(Z,W))))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,f(Z,f(Z,Y))),Z) )).
