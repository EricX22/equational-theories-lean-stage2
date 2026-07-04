% order5_0218  eq1=15983 eq2=22697  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,f(W,Y)),X),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(Y,Z)),f(f(Z,X),X)) )).
