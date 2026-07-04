% order5_0007  eq1=51460 eq2=3011  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(X,Z),f(X,Y)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,Z)),Y),X) )).
