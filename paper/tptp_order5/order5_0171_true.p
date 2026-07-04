% order5_0171  eq1=51104 eq2=14185  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(f(W,Z),W)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(f(Z,W),Z)),X)) )).
