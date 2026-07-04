% order5v2_0307  eq1=32678 eq2=43491  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,f(W,Z)),Y)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(X,X),f(Y,Z))) )).
