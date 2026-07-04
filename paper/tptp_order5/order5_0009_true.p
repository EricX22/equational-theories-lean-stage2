% order5_0009  eq1=17366 eq2=35665  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Y),f(Y,f(X,f(X,Z)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,f(X,Y)),f(Z,W)),W) )).
