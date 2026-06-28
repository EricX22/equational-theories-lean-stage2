% hard3_0074  eq1=545 eq2=1832  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(X,f(Z,X)))) )).
fof(goal, conjecture, ! [X] : ( X = f(f(X,f(X,X)),f(X,X)) )).
