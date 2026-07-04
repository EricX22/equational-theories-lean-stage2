% order5_0030  eq1=39421 eq2=10749  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(Y,Z),f(X,Y)),X),Y) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(f(Z,X),U))) )).
