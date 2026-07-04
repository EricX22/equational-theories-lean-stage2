% order5_0217  eq1=57898 eq2=14151  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(f(Y,X),X),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(f(Z,Y),Z)),Z)) )).
