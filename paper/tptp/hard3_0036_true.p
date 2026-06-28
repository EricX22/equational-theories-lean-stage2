% hard3_0036  eq1=204 eq2=1426  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(X,X)),Y) )).
fof(goal, conjecture, ! [X] : ( X = f(f(X,X),f(X,f(X,X))) )).
