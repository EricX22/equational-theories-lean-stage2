% order5_0177  eq1=333 eq2=19853  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( f(X,Y) = f(Y,f(X,Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,X),f(f(Y,f(X,Z)),W)) )).
