% hard3_0002  eq1=9 eq2=2441  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(X,Y)) )).
fof(goal, conjecture, ! [X] : ( X = f(f(X,f(f(X,X),X)),X) )).
