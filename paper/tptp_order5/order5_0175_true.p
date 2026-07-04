% order5_0175  eq1=44036 eq2=55124  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(W,X),f(W,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Y)) = f(Z,f(f(X,W),X)) )).
