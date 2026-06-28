% hard3_0318  eq1=2931 eq2=2484  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),W),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(f(Y,Z),Z)),X) )).
