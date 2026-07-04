% order5_0180  eq1=22505 eq2=46912  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(X,Y)),f(f(Z,Z),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,Y),f(f(Z,W),X)) )).
