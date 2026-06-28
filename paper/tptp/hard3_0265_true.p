% hard3_0265  eq1=2519 eq2=4405  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(X,Z),Y)),Z) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(X,Y)) = f(f(Y,X),X) )).
