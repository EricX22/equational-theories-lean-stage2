% order5v2_1668  eq1=2309 eq2=17200  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(Y,Z))),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,X),f(X,f(Z,f(Y,X)))) )).
