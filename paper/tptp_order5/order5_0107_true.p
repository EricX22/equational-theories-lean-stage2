% order5_0107  eq1=55251 eq2=45799  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(X,f(f(W,Z),Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(f(W,Y),X),X)) )).
