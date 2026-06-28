% hard3_0290  eq1=2696 eq2=203  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(Y,X),f(X,X)),X) )).
fof(goal, conjecture, ! [X] : ( X = f(f(X,f(X,X)),X) )).
