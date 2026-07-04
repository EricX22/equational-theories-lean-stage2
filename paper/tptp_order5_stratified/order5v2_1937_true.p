% order5v2_1937  eq1=14998 eq2=43016  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,Y),f(W,U)),W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(Y,f(f(Y,Z),W))) )).
