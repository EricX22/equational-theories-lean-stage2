% order5_0006  eq1=49823 eq2=15414  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( f(X,Y) = f(f(Y,f(Y,f(Y,X))),X) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(f(f(Y,f(Z,W)),W),W)) )).
