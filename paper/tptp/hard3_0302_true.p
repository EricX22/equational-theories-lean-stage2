% hard3_0302  eq1=2852 eq2=2886  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(X,f(X,Y)),X),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),Y),X) )).
