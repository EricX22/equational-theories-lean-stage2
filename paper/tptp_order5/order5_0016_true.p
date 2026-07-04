% order5_0016  eq1=49239 eq2=30798  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(f(Z,Z),Z),f(X,Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(f(Z,X),Z))),W) )).
