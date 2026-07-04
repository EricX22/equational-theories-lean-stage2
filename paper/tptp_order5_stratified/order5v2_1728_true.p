% order5v2_1728  eq1=49017 eq2=45260  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(f(Y,Z),Z),f(Z,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(f(X,Z),X),X)) )).
